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

  async function generateQuestion(input) {
    const response = await fetch(`${BASE_URL}/generate-question`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question: input }),
    });

    const data = await response.json();
    return data.answer;
  }

  const handleNewQuery = async (e) => {
    e.preventDefault();

    if (!newUserQuery.trim()) return;

    setLoading(true);
    try {
      const response = await generateQuestion(newUserQuery.trim());
      setAnswer(response);
    } catch (error) {
      console.error("Failed to get question:", error);
      setAnswer("Sorry, something went wrong. Please try again.");
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
        <form onSubmit={handleNewQuery} className="space-y-4">
          <div>
            <Input
              id="userchatinput"
              type="text"
              value={newUserQuery}
              onChange={(e) => setNewUserQuery(e.target.value)}
              required
            />
          </div>
        </form>

        {answer && (
            <div className="mt-4 p-4 bg-gray-100 rounded">
                <strong>Assistant:</strong> {answer}
            </div>
        )}
      </CardContent>
    </Card>
  );
};

export default Questions;