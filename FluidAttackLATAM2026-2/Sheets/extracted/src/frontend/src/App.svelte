<script lang="ts">
  import { SvelteToast } from "@zerodevx/svelte-toast";

  import Router from "./components/DOMRouter.svelte";
  import IndexPage from "./components/IndexPage.svelte";
  import Link from "./components/Link.svelte";
  import ProfileSettingsPage from "./components/ProfileSettingsPage.svelte";
  import SheetPage from "./components/SheetPage.svelte";

  const routes: any = {
    "/": IndexPage,
    "/sheets": SheetPage,
    "/settings": ProfileSettingsPage,
  };
</script>

<svelte:head>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sheets</title>
</svelte:head>

<div class="app">
  <header class="header">
    <div class="container header-inner">
      <Link href="/" class="brand">Sheets</Link>
      <nav class="nav">
        {#each Object.keys(routes) as routeLink}
          <Link href={routeLink}
            >{routeLink === "/"
              ? "Home"
              : routeLink.toUpperCase().at(1) +
                routeLink.toLowerCase().substring(2)}</Link
          >
        {/each}
      </nav>
    </div>
  </header>

  <main class="container main">
    <Router {routes} />
  </main>
  <SvelteToast />
</div>
