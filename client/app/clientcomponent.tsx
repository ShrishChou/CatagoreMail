"use client";

import React from "react";
import { useUser } from "@clerk/nextjs";

interface TrainingResult {
  message: string;
  texts: string[];
  actual_labels: string[];
  predicted_labels: string[];
}

export default function ClientComponent({
  flaskApiResponse,
}: {
  flaskApiResponse: TrainingResult | null;
}) {
  const { isSignedIn, user } = useUser();

  if (!isSignedIn) {
    return (
      <div className="text-center py-10">
        <p>Please sign in to view the results.</p>
      </div>
    );
  }

  if (!flaskApiResponse) {
    return (
      <div className="text-center py-10">
        <p>No data available. Please run the training process.</p>
      </div>
    );
  }

  return (
    <div>
      <div>{flaskApiResponse.message}</div>
      <div>
        {flaskApiResponse.texts && flaskApiResponse.texts.length > 0 ? (
          <ul>
            {flaskApiResponse.texts.map((text, index) => (
              <li key={index} className="mb-4">
                <strong>Text:</strong> {text.substring(0, 100)}...
                <br />
                <strong>Actual Label:</strong>{" "}
                {flaskApiResponse.actual_labels[index]}
                <br />
                <strong>Predicted Label:</strong>{" "}
                {flaskApiResponse.predicted_labels[index]}
              </li>
            ))}
          </ul>
        ) : (
          <p>No results to display</p>
        )}
      </div>
    </div>
  );
}
