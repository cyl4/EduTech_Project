
import { useState, useEffect } from 'react';
import React from "react";
import { Button } from "@/components/ui/button";
import { useRef } from 'react';
import { BASE_URL } from "../../../config";
import Questions from '../components/Questions';

const Dashboard = () => {
  const [count, setCount] = useState(0);
  const [mode, setMode] = useState('professional');
  const [topic, setTopic] = useState('');
  const [customPrompt, setCustomPrompt] = useState('');
  const [transcript, setTranscript] = useState('');
  const [questions, setQuestions] = useState([]);

  // Voice recording state
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  useEffect(() => {
    // autofocus topic on mount
    const el = document.getElementById('topic');
    el?.focus();
  }, []);

  // Voice recording handlers
  const startRecording = async () => {
    if (!navigator.mediaDevices) {
      alert('Audio recording not supported in this browser.');
      return;
    }
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new window.MediaRecorder(stream);
    audioChunksRef.current = [];
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) audioChunksRef.current.push(e.data);
    };
    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
      setAudioURL(URL.createObjectURL(audioBlob));
      // Send audio to backend and get transcript
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.webm');
      const response = await fetch(`${BASE_URL}/analyze-audio`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setTranscript(data.transcription || '');
      // Send transcript to question generator
      const questionRes = await fetch(`${BASE_URL}/generate-questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          transcript: data.transcription || '',
          topic: topic || '',
          mode: mode || 'professional',
        }),
      });
      const questionData = await questionRes.json();
      setQuestions(questionData.questions || []);
    };
    mediaRecorderRef.current = mediaRecorder;
    mediaRecorder.start();
    setRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };




  const MODES = [
    { id: 'professional', label: 'Professional', hint: 'Professional presentation style, perfect for collegiate and professional presentations.' },
    { id: 'technical',    label: 'Technical',    hint: 'For professional users well versed in their respective field, familiar with jargon, low-level knowledge of topics.' },
    { id: 'layperson',    label: 'Layperson',    hint: 'For beginners to the topic, child-friendly, minimal jargon.' },
    { id: 'casual',       label: 'Casual',       hint: 'Friendly, conversational tone for casual practice.' },
    { id: 'custom',       label: 'Custom',       hint: 'Use your own style & instructions.' },
  ];

  function handleCreateSession() {
    const stamp = new Date().toLocaleString();
    const tone = mode === 'custom' && customPrompt.trim()
      ? `custom → ${customPrompt.trim()}`
      : mode;
    const seed = `\n[${stamp}] New session #${count + 1}\n• Mode: ${tone}\n• Topic: ${topic || '(none)'}\n`;
    setTranscript(prev => (prev ? prev + "\n" + seed : seed));
    setCount(c => c + 1);
    // Hook this to your Node backend:
    // await fetch('/api/session', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ mode, topic, customPrompt })
    // })
  }

  function handleCopy() {
    if (!transcript) return;
    navigator.clipboard?.writeText(transcript);
  }

  function handleClearTranscript() {
    setTranscript('');
  }

  const activeHint = MODES.find(m => m.id === mode)?.hint;

  return (
    <div className="flex min-h-svh flex-col items-center justify-center bg-gradient-to-b from-background to-muted/30 p-6">
      <div className="w-full max-w-5xl">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">Presentation Prep Assistant</h1>
          </div>
        </div>

        {/* Voice Recorder */}
          <div className="mb-6 flex flex-col items-center">
            <h2 className="text-lg font-medium mb-2">Voice Recorder</h2>
            <div className="flex gap-3">
              {!recording ? (
                <Button onClick={startRecording} variant="secondary">Start Recording</Button>
              ) : (
                <Button onClick={stopRecording} variant="destructive">Stop Recording</Button>
              )}
            </div>
            {audioURL && (
              <audio controls src={audioURL} className="mt-4" />
            )}
            {transcript && (
              <div className="mt-4 p-2 bg-gray-100 rounded w-full max-w-xl">
                <strong>Transcript:</strong> {transcript}
              </div>
            )}
            {questions.length > 0 && (
              <div className="mt-4 p-4 bg-gray-100 rounded w-full max-w-xl">
                <strong>Generated Questions:</strong>
                <ul>
                  {questions.map((q, i) => <li key={i}>{q.question}</li>)}
                </ul>
              </div>
            )}
          </div>

        <div className="grid gap-6 md:grid-cols-2">
          {/* Left: Controls */}
          <section className="rounded-2xl border bg-card shadow-sm">
            <div className="border-b p-5">
              <h2 className="text-lg font-medium">Session Setup</h2>
              <p className="text-sm text-muted-foreground">Pick a mode, add a topic, then create a session.</p>
            </div>

            <div className="space-y-5 p-5">
              {/* Modes */}
              <div className="space-y-2">
                <label className="text-xs uppercase tracking-wide text-muted-foreground">Mode</label>
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-5">
                  {MODES.map(m => (
                    <label
                      key={m.id}
                      className={`flex cursor-pointer items-center justify-center rounded-xl border px-3 py-2 text-sm transition ${
                        mode === m.id ? 'border-primary ring-1 ring-primary' : 'hover:bg-muted'
                      }`}
                    >
                      <input
                        type="radio"
                        name="mode"
                        value={m.id}
                        checked={mode === m.id}
                        onChange={(e) => setMode(e.target.value)}
                        className="peer sr-only"
                      />
                      {m.label}
                    </label>
                  ))}
                </div>
                <p className="text-sm text-muted-foreground">{activeHint}</p>
              </div>

              {/* Topic */}
              <div className="space-y-2">
                <label htmlFor="topic" className="text-sm font-medium">Topic</label>
                <input
                  id="topic"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="e.g., Bias in machine learning models: causes, consequences, and solutions"
                  className="w-full rounded-xl border bg-background px-3 py-2 outline-none ring-0 transition focus:border-primary"
                />
              </div>

              {/* Custom instructions */}
              {mode === 'custom' && (
                <div className="space-y-2">
                  <label htmlFor="custom" className="text-sm font-medium">Custom Instructions</label>
                  <textarea
                    id="custom"
                    value={customPrompt}
                    onChange={(e) => setCustomPrompt(e.target.value)}
                    placeholder="e.g., Be direct. Use numbered steps. Include speaker notes and a TL;DR."
                    className="min-h-[96px] w-full rounded-xl border bg-background px-3 py-2 outline-none focus:border-primary"
                  />
                </div>
              )}

              {/* Actions */}
              <div className="flex flex-wrap items-center gap-3 pt-1">
                <Button onClick={handleCreateSession} className="gap-2">Create Session</Button>
                <Button variant="secondary" onClick={() => setTopic('')}>Clear Topic</Button>
                <span className="text-sm text-muted-foreground">Sessions: <strong>{count}</strong></span>
              </div>

              <div className="rounded-xl border bg-muted/30 p-3 text-sm text-muted-foreground">
                <Questions />
              </div>
            </div>
          </section>

          {/* Right: Transcript Output */}
          <section className="rounded-2xl border bg-card shadow-sm">
            <div className="border-b p-5">
              <h2 className="text-lg font-medium">Transcript Output</h2>
              <p className="text-sm text-muted-foreground">Session events and streamed responses will appear here.</p>
            </div>

            <div className="flex h-full flex-col p-5">
              <div className="flex items-center gap-3 pb-3">
                <Button variant="secondary" onClick={handleCopy}>Copy</Button>
                <Button variant="destructive" onClick={handleClearTranscript}>Clear</Button>
              </div>
               <div className="relative min-h-[260px] w-full overflow-hidden rounded-xl border bg-background">
                <pre className="max-h-[420px] whitespace-pre-wrap break-words p-4 text-sm text-muted-foreground">
{transcript || 'Transcript will appear here…'}
                </pre>
              </div>
            </div>
          </section>
        </div>
      </div>

    </div>
  )



}


export default Dashboard;