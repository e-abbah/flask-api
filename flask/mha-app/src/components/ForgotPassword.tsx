import { useState } from "react";
import { Link } from "react-router-dom";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleForgotPassword(e: React.FormEvent) {
    e.preventDefault();

    setLoading(true);
    setMessage("");
    setError("");

    try {
      const response = await fetch(
        "https://flask-api-chqu.onrender.com/api/auth/forgot-password",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message);
        setEmail("");
      } else {
        setError(data.message || "Something went wrong.");
      }
    } catch (error) {
      console.error(error);
      setError("Unable to connect to the server.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      className="h-screen w-screen bg-cover bg-center flex items-center justify-center px-4 sm:px-6 lg:px-8"
      style={{ backgroundImage: "url('/Background.jpg')" }}
    >
      <div className="w-full max-w-md bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl p-8">
        <h2 className="text-white text-3xl sm:text-4xl font-bold mb-6 text-center drop-shadow-lg">
          FORGOT PASSWORD
        </h2>

        <p className="text-white text-center mb-8">
          Enter your email address and we'll send you a password reset link.
        </p>

        <form
          className="flex flex-col gap-4"
          onSubmit={handleForgotPassword}
        >
          <input
            type="email"
            placeholder="Email address"
            className="p-3 rounded-xl border border-white bg-white/20 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <button
            type="submit"
            className="bg-blue-500 text-white py-3 rounded-xl font-semibold hover:bg-blue-600 transition disabled:bg-gray-500 disabled:cursor-not-allowed"
            disabled={loading}
          >
            {loading ? "Sending..." : "Send Reset Link"}
          </button>
        </form>

        {message && (
          <p className="text-green-300 text-sm text-center mt-4">
            {message}
          </p>
        )}

        {error && (
          <p className="text-red-300 text-sm text-center mt-4">
            {error}
          </p>
        )}

        <p className="text-sm mt-6 text-center text-white drop-shadow-md">
          Remember your password?{" "}
          <Link to="/login" className="underline">
            Log In
          </Link>
        </p>
      </div>
    </div>
  );
}

