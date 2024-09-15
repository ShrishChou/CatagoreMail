"use client";

import React, { useEffect, useState } from "react";
interface Email {
  subject: string;
  sender: string;
  body: string;
}

export default function ClientComponent({
  initialEmails,
}: {
  initialEmails: Email[];
}) {
  const [message, setMessage] = useState("Loading");
  const [emails, setEmails] = useState<Email[]>(initialEmails);

  useEffect(() => {
    fetch("http://localhost:8080/api/train")
      .then((response) => response.json())
      .then((data) => {
        setMessage(data.message);
      })
      .catch((error) => {
        console.error("Error fetching training data:", error);
        setMessage("Error loading training data");
      });
  }, []);

  const handleButtonClick = async () => {
    try {
      //   const newEmails = await getInitialEmails();
      //   setEmails(newEmails);
    } catch (error) {
      console.error("Error fetching emails:", error);
      setEmails([]);
      setMessage("Error occurred while fetching emails");
    }
  };

  return (
    <div>
      <div>{message}</div>
      <button onClick={handleButtonClick}>Refresh Emails</button>
      <div>
        {emails.length > 0 ? (
          <ul>
            {emails.map((email, index) => (
              <li key={index}>
                <strong>Subject:</strong> {email.subject}
                <br />
                <strong>From:</strong> {email.sender}
                <br />
                <strong>Body:</strong> {email.body.substring(0, 100)}...
              </li>
            ))}
          </ul>
        ) : (
          <p>No emails to display</p>
        )}
      </div>
    </div>
  );
}
