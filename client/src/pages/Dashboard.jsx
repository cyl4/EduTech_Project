import React, { useEffect, useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";

// your original component (untouched)
const Dashboard = () => {
    const navigate = useNavigate();
    const [error, setError] = useState("");

    return (
        <div>
            {/* dashboard content goes here */}
        </div>
    );
};

// auth popup
const AuthPopup = () => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState("login");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (username && password) {
            navigate("/dashboard");
        }
    };

    return (
        <div className="flex h-screen w-screen items-center justify-center bg-gradient-to-br from-gray-100 to-blue-100">
            <div className="backdrop-blur-xl bg-white/80 border border-gray-200 rounded-2xl shadow-lg w-full max-w-md p-8">
                {/* tabs */}
                <div className="flex justify-around mb-6">
                    <button
                        className={`w-1/2 py-2 rounded-lg font-medium transition ${
                            activeTab === "login"
                                ? "bg-gray-300 text-gray-800"
                                : "bg-transparent text-gray-500 hover:bg-gray-100"
                        }`}
                        onClick={() => setActiveTab("login")}
                    >
                        Log In
                    </button>
                    <button
                        className={`w-1/2 py-2 rounded-lg font-medium transition ${
                            activeTab === "signup"
                                ? "bg-gray-300 text-gray-800"
                                : "bg-transparent text-gray-500 hover:bg-gray-100"
                        }`}
                        onClick={() => setActiveTab("signup")}
                    >
                        Sign Up
                    </button>
                </div>

                {/* form */}
                <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="px-4 py-3 rounded-lg bg-white border border-gray-200 text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300"
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="px-4 py-3 rounded-lg bg-white border border-gray-200 text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300"
                    />
                    <button
                        type="submit"
                        className="py-3 rounded-lg bg-blue-200 hover:bg-blue-300 text-gray-800 font-medium shadow transition"
                    >
                        {activeTab === "login" ? "Log In" : "Sign Up"}
                    </button>
                </form>
            </div>
        </div>
    );
};

// route setup
const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<AuthPopup />} />
            <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
    );
};

export default AppRoutes;
