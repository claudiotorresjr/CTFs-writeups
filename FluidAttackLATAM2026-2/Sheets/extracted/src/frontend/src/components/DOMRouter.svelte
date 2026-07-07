<script lang="ts">
  import { type Component, onMount } from "svelte";

  let { routes }: { routes: { [key: string]: Component } } = $props();
  let CurrentComponent = $state<Component>();
  let newRoute = $state("/");
  let appState = $state({});

  function syncRoute() {
    newRoute = window.location.hash.slice(1);

    if (newRoute === "") {
      location.href = "/#/";
      newRoute = "/";
    }

    if (routes.hasOwnProperty(newRoute)) {
      CurrentComponent = routes[newRoute];
    } else {
      CurrentComponent = undefined;
    }
  }

  onMount(() => {
    syncRoute();
  });
</script>

<svelte:window onhashchange={syncRoute} />

{#if CurrentComponent}
  <CurrentComponent {appState} />
{:else}
  <div id="Router">
    <h1>404 Not Found</h1>
    <p>Unmapped route: "{newRoute}"</p>
  </div>
{/if}
