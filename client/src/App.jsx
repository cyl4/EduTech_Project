import { useState, useEffect } from 'react'
import React from "react";
// import { Routes, Route } from "react-router-dom";
import { Button } from "@/components/ui/button"
import './App.css'

const App = () => {
  const [count, setCount] = useState(0)

  return (
  
    <div className="flex min-h-svh flex-col items-center justify-center">
      <Button>Click me</Button>
    </div>
  )
}

export default App;
