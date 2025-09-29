import { useState, useEffect } from 'react'
import React from "react";
import { Routes, Route } from "react-router-dom";
import { Button } from "@/components/ui/button"
import Dashboard from "./pages/Dashboard.jsx";
import Login from "./pages/Login.jsx";
import { Navigate } from "react-router-dom";
import './App.css'

const App = () => {

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/Login" replace />} />
      <Route path="/Login" element={<Login />} />
      <Route path="/Dashboard" element={<Dashboard />} />
    </Routes>
  )
 
}

export default App;
