module.exports = {
  content: [
    "./*.{html,md,markdown}",
    "./_layouts/**/*.{html,md,markdown}",
    "./_includes/**/*.{html,md,markdown}",
    "./_lore/**/*.{html,md,markdown}",
    "./_posts/**/*.{html,md,markdown}",
    "./_drafts/**/*.{html,md,markdown}",
    "./puzzles/**/*.{html,md,markdown}",
    "./assets/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        void: "#0b1020",
        panel: "#121a30",
        cyan: {
          trace: "#67e8f9"
        },
        amber: {
          warn: "#fbbf24"
        },
        red: {
          fault: "#f87171"
        },
        slate: {
          mutext: "#94a3b8"
        },
        phosphor: "#8fffc1",
        magenta: {
          quiet: "#d946ef"
        }
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "monospace"]
      },
      boxShadow: {
        terminal: "0 0 0 1px rgba(103, 232, 249, 0.16), 0 18px 60px rgba(0, 0, 0, 0.38)",
        glow: "0 0 24px rgba(103, 232, 249, 0.18)"
      },
      animation: {
        blink: "blink 1.1s steps(2, start) infinite",
        pulseSoft: "pulseSoft 2.8s ease-in-out infinite",
        scan: "scan 7s linear infinite"
      },
      keyframes: {
        blink: {
          "0%, 45%": { opacity: "1" },
          "46%, 100%": { opacity: "0" }
        },
        pulseSoft: {
          "0%, 100%": { opacity: "0.62", boxShadow: "0 0 0 rgba(103, 232, 249, 0)" },
          "50%": { opacity: "1", boxShadow: "0 0 14px rgba(103, 232, 249, 0.44)" }
        },
        scan: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100vh)" }
        }
      }
    }
  },
  plugins: []
};
