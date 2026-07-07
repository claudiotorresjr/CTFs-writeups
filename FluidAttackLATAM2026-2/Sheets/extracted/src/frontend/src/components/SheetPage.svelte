<script lang="ts">
  import { RevoGrid, type ColumnRegular } from "@revolist/svelte-datagrid";
  import { toast } from "@zerodevx/svelte-toast";
  import { onMount } from "svelte";

  let { appState } = $props();
  let error = $state("");
  let header: string[] = $state([]);
  let source: string[][] = $state([]);
  let columns: ColumnRegular[] = $state([]);
  let grid = $state();

  async function fetchSpreadsheet() {
    let data = await fetch("/api/sheets").then((r) => r.json());
    return data;
  }

  async function renderSpreadsheet() {
    try {
      let tableData = await fetchSpreadsheet();

      header = tableData.header;
      columns = header.map((h, idx) => {
        return { prop: idx, name: h ? h.toUpperCase() : "" };
      });
      source = tableData.rows;
    } catch (err) {
      console.log(err);
      error = err as string;
    }
  }

  async function updateSpreadsheet({
    header,
    rows,
  }: {
    header: string[];
    rows: string[][];
  }): Promise<{ header: string[]; rows: string[][] } | undefined> {
    let data = await fetch("/api/sheets", {
      method: "POST",
      body: JSON.stringify({ header, rows }),
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": appState.key,
      },
    }).then((r) => r.json());

    if (data.error || data.detail) {
      return data.error || data.detail;
    }

    return data;
  }

  onMount(async () => {
    await renderSpreadsheet();

    // sync and cache api write key
    let r: { key: string } = await fetch("/api/key").then((r) => r.json());
    if (r.key) {
      appState.key = r.key;
    } else {
      delete appState.key;
    }
  });

  async function handleColumnUpdate() {
    source = await (grid as any).getSource();

    try {
      const updatedTable = await updateSpreadsheet({ header, rows: source });

      if (!updatedTable || typeof updatedTable === "string") {
        // reset state on failure
        toast.push(updatedTable || "Unknown error, updated failed.");
        renderSpreadsheet();

        return;
      }

      try {
        if (updatedTable.rows) {
          source = updatedTable.rows;
          // re-run for formula evaluation
          await renderSpreadsheet();
          toast.push("Spreadsheet updated successfully");
        } else {
          toast.push(
            (updatedTable as any).detail || (updatedTable as any).error
          );
        }
      } catch (e) {
        toast.push(e + "");
      }
    } catch (e) {
      toast.push(e + "");
    }
  }
</script>

<section class="panel">
  <h1>Sheets View</h1>

  <div class="table">
    <RevoGrid bind:this={grid} {source} {columns}></RevoGrid>
  </div>
  <button onclick={handleColumnUpdate}>Save Changes</button>
</section>

<style>
  .table {
    background: #efefef;
    margin-bottom: 1rem;
  }
</style>
