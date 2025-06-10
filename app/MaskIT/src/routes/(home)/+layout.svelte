<script>
  import { onMount } from "svelte";
  import { page } from '$app/stores';  
  import Navbar from "./Navbar.svelte";
  import BottomNav from "./BottomNav.svelte";

</script>

<Navbar />

<slot />

<BottomNav />
