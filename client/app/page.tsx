import { auth, clerkClient } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";
import { google } from "googleapis";
import ClientComponent from "./clientcomponent";
import { load } from "cheerio";

async function getGmailService() {
  const { userId } = auth();
  if (!userId) {
    throw new Error("User not found");
  }
  const clerkResponse = await clerkClient.users.getUserOauthAccessToken(
    userId,
    "oauth_google"
  );
  if (!clerkResponse.data || clerkResponse.data.length === 0) {
    throw new Error("No OAuth token found");
  }
  const token = clerkResponse.data[0].token;
  return google.gmail({
    version: "v1",
    headers: { Authorization: `Bearer ${token}` },
  });
}

function decodeEmailBody(payload: any): string {
  function base64UrlDecode(data: string): string {
    return Buffer.from(data, "base64").toString("utf-8");
  }

  if (payload.body && payload.body.data) {
    return base64UrlDecode(payload.body.data);
  }

  const parts = payload.parts || [];
  for (const part of parts) {
    if (part.mimeType === "text/plain" && part.body && part.body.data) {
      return base64UrlDecode(part.body.data);
    } else if (part.mimeType === "text/html" && part.body && part.body.data) {
      const htmlContent = base64UrlDecode(part.body.data);
      const $ = load(htmlContent);
      return $.text();
    }
  }

  return "No body content";
}

async function fetchEmailData(gmail: any, messageId: string, read: number) {
  const msg = await gmail.users.messages.get({
    userId: "me",
    id: messageId,
    format: "full",
  });
  const headers = msg.data.payload.headers;

  const subject =
    headers.find((header: any) => header.name === "Subject")?.value ||
    "No Subject";
  const sender =
    headers.find((header: any) => header.name === "From")?.value || "No Sender";
  const body = decodeEmailBody(msg.data.payload);

  return { subject, sender, body, read };
}
async function getGmailLabels() {
  try {
    const { userId } = auth();
    if (!userId) {
      return { message: "User not found" };
    }
    const clerkResponse = await clerkClient.users.getUserOauthAccessToken(
      userId,
      "oauth_google"
    );
    if (clerkResponse.data && clerkResponse.data.length > 0) {
      const token = clerkResponse.data[0].token;
      const gmail = google.gmail({
        version: "v1",
        headers: { Authorization: `Bearer ${token}` },
      });
      const res = await gmail.users.labels.list({
        userId: "me",
      });
      return res.data.labels;
    } else {
      return { message: "No OAuth token found" };
    }
  } catch (error) {
    console.log("[GMAIL ERROR]", error);
    return { message: "Internal error" };
  }
}

async function fetchEmails(gmail: any, query: string, maxResults: number) {
  let emails: any = [];
  let pageToken = null;

  while (emails.length < maxResults) {
    const results: any = await gmail.users.messages.list({
      userId: "me",
      q: query,
      maxResults: 100,
      pageToken: pageToken,
    });

    const messages = results.data.messages || [];
    pageToken = results.data.nextPageToken;

    emails = emails.concat(messages);

    if (emails.length >= maxResults || !pageToken) {
      break;
    }
  }

  return emails.slice(0, maxResults);
}
export async function getInitialEmails(read: number) {
  // This function should contain the logic from your GET function in the API route
  // ...

  try {
    let query = "";
    if (read == 1) {
      query = "is:read";
    } else {
      query = "is:unread";
    }
    const gmail = await getGmailService();
    const totalRead = 100;
    const readMessages = await fetchEmails(gmail, query, totalRead);

    if (readMessages.length > 0) {
      let readEmails = [];
      for (let idx = 0; idx < readMessages.length; idx++) {
        const emailData = await fetchEmailData(
          gmail,
          readMessages[idx].id,
          read
        );
        readEmails.push(emailData);
      }
      return readEmails;
    }

    return [];
  } catch (error) {
    console.error("[GMAIL ERROR]", error);
    return [];
  }
}

async function sendEmailsToFlaskAPI(emails: any[]) {
  try {
    const response = await fetch("http://localhost:8080/api/train", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ emails }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log("Flask API response:", result);
    return result;
  } catch (error) {
    console.error("Error sending emails to Flask API:", error);
    throw error;
  }
}

export default async function Page() {
  let flaskApiResponse = null;
  try {
    const { userId } = auth();
    let flaskApiResponse = null;
    if (userId) {
      try {
        const initialReadEmails = await getInitialEmails(1);
        const initialUnreadEmails = await getInitialEmails(0);
        const initialEmails = initialReadEmails.concat(initialUnreadEmails);
        flaskApiResponse = await sendEmailsToFlaskAPI(initialEmails);
      } catch (error) {
        console.error("Failed to send emails to Flask API:", error);
      }
    }
  } catch (error) {
    console.error("Failed to send emails to Flask API:", error);
  }
  return (
    <ClientComponent
      flaskApiResponse={flaskApiResponse}
      // initialEmails={initialEmails}
    />
  );
}
