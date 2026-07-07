<script lang="ts">
  import { onMount } from "svelte";

  let { appState } = $props();

  onMount(async () => {
    if (!appState.whoami) {
      let r = await fetch("/api/whoami").then((r) => r.json());
      appState.whoami = r;
    }
  });

  async function handleSubmit(this: HTMLFormElement, event: SubmitEvent) {
    event.preventDefault();

    let formData = new FormData(this);

    let _whoami = await fetch(this.action, {
      method: this.method,
      body: JSON.stringify({ new_username: formData.get("new_username") }),
      headers: { "Content-Type": "application/json" },
    }).then((r) => r.json());

    appState.whoami = _whoami;
  }
</script>

<section class="panel">
  <h1>Overview</h1>
  {@html `<textarea disabled rows="5" style="width:450px;resize:none;">${
    appState.whoami
      ? JSON.stringify(appState.whoami, undefined, 2).replace("<", "")
      : "Loading..."
  } 
  </textarea>`}
</section>

<section class="panel">
  <h1>Update Profile</h1>

  <form method="POST" action="/api/whoami" onsubmit={handleSubmit}>
    <label for="new_username">
      New Username
      <input
        id="new_username"
        name="new_username"
        type="text"
        value={appState.whoami?.username}
      />
    </label>
    <input class="button" type="submit" value="Update" />
  </form>
</section>

<style>
  form {
    max-width: 400px;
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  label {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .button {
    align-self: self-start;
  }
</style>
