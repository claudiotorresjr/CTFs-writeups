<script>
let props = $props();
let href = props.href ? "/#/" + props.href.replace(/^\/+/, '') : "";
</script>

<a {...props} {href}>{@render props.children?.()}</a>
