import {useState} from "react";
//import {useNavigate} from "react-router-dom";
import {Link} from "react-router-dom";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [fullname, setFullname] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  //const navigate = useNavigate();

  async function handleLogin(e: React.FormEvent) {
  e.preventDefault();
  setLoading(true);

  try {
    const response = await fetch("https://flask-api-chqu.onrender.com/api/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, fullname, password }),
    });

    const data = await response.json();

    if (response.ok) {
      // window.alert(`Sign up successful: ${data.message}`);
      <Link to="/login" className="underline">
        Log in
        </Link>
    } else {
      window.alert(`Sign up failed: ${data.message}`);
    }
  } catch (error) {
    console.error(error);
    window.alert("Unable to connect to the server");
  } finally {
    setEmail("");
    setPassword("");
    setFullname("");
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
          SIGN UP
        </h2>
        <p className="text-white text-center ">Create an account here to start</p>
        <form className="flex flex-col gap-4">
          <input
            type="email"
            placeholder="email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="p-3 rounded-xl border  border-white bg-white/20 mt-6 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
             <input
            type="fullname"
            value={fullname}
            onChange={(e) => setFullname(e.target.value)}
            placeholder="Full Name"
            className="p-3 rounded-xl border border-white bg-white/20 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="p-3 rounded-xl border border-white bg-white/20 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
            onClick={handleLogin}
            disabled={loading}
            className="bg-blue-500 text-white py-3 rounded-xl font-semibold hover:bg-blue-600 transition disabled:bg-gray-500 disabled:cursor-not-allowed"
          >
           {loading ? "Signing up..." : "Sign Up"}
          </button>
        </form>

        <p className="text-sm mt-4 text-center text-white drop-shadow-md">
          Already have an account? {""}
          <a href="/login" className="underline">
            Log in
          </a>
        </p>
      </div>
    </div>
  );
}
