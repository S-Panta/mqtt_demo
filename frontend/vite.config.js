import { defineConfig } from 'vite';

export default defineConfig({
  optimizeDeps: {
    include: ['chartjs-adapter-date-fns'],
  },
});
