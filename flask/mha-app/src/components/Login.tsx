import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(
        "https://flask-api-chqu.onrender.com/api/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, password }),
        },
      );

      const data = await response.json();

      if (response.ok) {
        window.alert(`Login successful: ${data.message}`);
      } else {
        window.alert(`Login failed: ${data.message}`);
      }
    } catch (error) {
      console.error(error);
      window.alert("Unable to connect to the server");
    } finally {
      setEmail("");
      setPassword("");
      setLoading(false);
    }
  }

  return (
    <div
      className="h-screen w-screen bg-cover bg-center flex items-center justify-center px-4 sm:px-6 lg:px-8"
      style={{ backgroundImage: "url('/Background.jpg')" }}
    >
      <div className="w-full max-w-md bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl p-8">
        <h2 className="text-white text-3xl sm:text-4xl font-bold mb-10 text-center drop-shadow-lg">
          LOG IN
        </h2>
        <p className="text-white text-center ">Welcome back! We missed you</p>
        <form className="flex flex-col gap-4" onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="email address"
            className="p-3 rounded-xl border  border-white bg-white/20 mt-6 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            className="p-3 rounded-xl border border-white bg-white/20 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            type="submit"
            className="bg-blue-500 text-white py-3 rounded-xl font-semibold hover:bg-blue-600 transition  disabled:bg-gray-500 disabled:cursor-not-allowed"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Log In"}
          </button>
        </form>
        <p className="text-sm mt-4 text-center text-white drop-shadow-md">
          Don't have an account?{" "}
          <a href="/" className="underline">
            Sign Up
          </a>
          <span className="mx-2">•</span>
          <a href="/forgot-password" className="underline">
            Forgot password?
          </a>
        </p>
      </div>
    </div>
  );
}
