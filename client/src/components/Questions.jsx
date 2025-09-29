import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { BASE_URL } from "../../../config";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const Questions = () => {
  const [newUserQuery, setNewUserQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState([]);

  async function generateQuestions({ transcript, topic, mode }) {
  const response = await fetch(`${BASE_URL}/generate-questions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ transcript, topic, mode }),
  });
  const data = await response.json();
  return data.questions;
}

  const handleNewQuery = async (e) => {
  e.preventDefault();
  if (!newUserQuery.trim()) return;
  setLoading(true);
  try {
    const result = await generateQuestions({
      transcript: "", // or your transcript value
      topic: newUserQuery.trim(),
      mode: "professional", // or user-selected mode
    });
    setQuestions(result);
  } catch (error) {
    setQuestions([{ question: "Sorry, something went wrong. Please try again." }]);
  }
  setLoading(false);
  setNewUserQuery("");
};

  return (
    <Card className="mb-8">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl">
          Question Generator 
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {questions.length > 0 && (
            <div className="mt-4 p-4 bg-gray-100 rounded">
    <strong>Generated Questions:</strong>
    <ul>
      {questions.map((q, i) => <li key={i}>{q.question}</li>)}
    </ul>
  </div>
        )}
      </CardContent>
    </Card>
  );
};

export default Questions;