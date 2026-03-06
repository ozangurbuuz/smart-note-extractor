/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          deep: "#0f172a",
          accent: "#0ea5e9",
          soft: "#e0f2fe"
        }
      }
    }
  },
  plugins: []
};
