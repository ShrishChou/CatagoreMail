import { auth, clerkClient } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";
import { google } from "googleapis";
import ClientComponent from "./clientcomponent";

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

export default async function Page() {
  const gmailLabels = await getGmailLabels();

  return <ClientComponent initialGmailLabels={gmailLabels} />;
}
