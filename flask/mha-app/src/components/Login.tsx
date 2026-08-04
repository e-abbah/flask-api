export default function Login() {
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
        <form className="flex flex-col gap-4">
          <input
            type="email"
            placeholder="email address"
            className="p-3 rounded-xl border  border-white bg-white/20 mt-6 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            type="password"
            placeholder="Password"
            className="p-3 rounded-xl border border-white bg-white/20 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white py-3 rounded-xl font-semibold hover:bg-blue-600 transition"
          >
            LOG IN
          </button>
        </form>

        <p className="text-sm mt-4 text-center text-white drop-shadow-md">
          Don't have an account? {""}
          <a href="/" className="underline">
            Sign Up
          </a>
        </p>
        
      </div>
    </div>
  );
}