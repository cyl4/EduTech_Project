import { useState, useEffect } from 'react'
import React from "react";
// import { Routes, Route } from "react-router-dom";
import { Button } from "@/components/ui/button"
import Dashboard from "./pages/Dashboard.jsx";
import Login from "./pages/Login.jsx";
import './App.css'

const App = () => {

  return (
    <Routes>
      <Route path={`/Login`} element={<Login />}></Route>
      <Route path={`/Dashboard`} element={<Dashboard />} />
    </Routes>
  )
 
}

export default App;
