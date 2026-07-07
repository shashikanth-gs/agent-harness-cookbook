# Deployment on a Personal Domain

The demo site is a static Vite app. Build it with:

```bash
npm --prefix apps/demo-site run build
```

Deploy `apps/demo-site/dist` to any static host. For a personal domain, configure
your DNS provider to point the domain or subdomain to the static host, then set
the host's custom domain setting.

The local FastAPI API is for demos. A static-only hosted site can show docs and
mock examples without running the API.
