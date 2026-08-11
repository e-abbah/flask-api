import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

export default function ResetPassword() {
  const { token } = useParams();
  const navigate = useNavigate();

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleResetPassword(e: React.FormEvent) {
    e.preventDefault();

    setMessage("");
    setError("");

    if (!token) {
      setError("Invalid or missing reset token.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `https://flask-api-chqu.onrender.com/api/auth/reset-password/${token}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            new_password: password,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setMessage("Password reset successful! Redirecting to login...");

        setPassword("");
        setConfirmPassword("");

        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } else {
        setError(data.message || "Unable to reset password.");
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
          RESET PASSWORD
        </h2>

        <p className="text-white text-center mb-8">
          Enter your new password below.
        </p>

        <form
          className="flex flex-col gap-4"
          onSubmit={handleResetPassword}
        >
          <input
            type="password"
            placeholder="New password"
            className="p-3 rounded-xl border border-white bg-white/20 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Confirm new password"
            className="p-3 rounded-xl border border-white bg-white/20 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />

          <button
            type="submit"
            className="bg-blue-500 text-white py-3 rounded-xl font-semibold hover:bg-blue-600 transition disabled:bg-gray-500 disabled:cursor-not-allowed"
            disabled={loading}
          >
            {loading ? "Resetting..." : "Reset Password"}
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

