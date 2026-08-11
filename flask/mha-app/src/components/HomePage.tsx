import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div
      className="min-h-screen w-full bg-cover bg-center"
      style={{ backgroundImage: "url('/Background.jpg')" }}
    >
      {/* Overlay */}
      <div className="min-h-screen bg-black/40">
        {/* Navbar */}
        <nav className="w-full px-6 py-5">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <Link
              to="/"
              className="text-2xl font-bold text-white drop-shadow-lg"
            >
              Aspira
            </Link>

            <div className="flex items-center gap-4">
              <Link
                to="/login"
                className="text-white font-medium hover:text-blue-200 transition"
              >
                Log In
              </Link>

              <Link
                to="/signup"
                className="bg-blue-500 hover:bg-blue-600 text-white px-5 py-2.5 rounded-xl font-semibold transition"
              >
                Sign Up
              </Link>
            </div>
          </div>
        </nav>

        {/* Hero */}
        <main className="min-h-[calc(100vh-88px)] flex items-center justify-center px-6">
          <div className="max-w-3xl text-center text-white">

            <p className="text-blue-200 font-semibold tracking-wide uppercase mb-4">
              Your journey starts here
            </p>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold leading-tight drop-shadow-xl">
              Discover opportunities.
              <br />
              <span className="text-blue-300">
                Build your future.
              </span>
            </h1>

            <p className="mt-6 text-lg sm:text-xl text-white/90 max-w-2xl mx-auto leading-relaxed drop-shadow-md">
              Aspira helps you discover opportunities, connect with the right
              support, and take the next step toward your goals.
            </p>

            {/* CTA */}
            <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                to="/signup"
                className="w-full sm:w-auto bg-blue-500 hover:bg-blue-600 text-white px-8 py-3.5 rounded-xl font-semibold text-lg transition shadow-lg"
              >
                Get Started
              </Link>

              <Link
                to="/login"
                className="w-full sm:w-auto border border-white/70 hover:bg-white/10 text-white px-8 py-3.5 rounded-xl font-semibold text-lg transition"
              >
                Log In
              </Link>
            </div>

            {/* Small supporting text */}
            <p className="mt-8 text-sm text-white/70">
              Create your account and start exploring what's possible.
            </p>
          </div>
        </main>
      </div>
    </div>
  );
}

