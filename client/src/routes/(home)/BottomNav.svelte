<script>
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { jwtDecode } from "jwt-decode";

  let prevScrollPos = 0;
  let isNavHidden = false;

  onMount(() => {
    const handleScroll = () => {
      const currentScrollPos = window.pageYOffset;

      if (prevScrollPos > currentScrollPos) {
        // Scrolling up
        isNavHidden = false;
      } else {
        // Scrolling down
        isNavHidden = true;
      }

      prevScrollPos = currentScrollPos;
    };

    window.addEventListener("scroll", handleScroll);

    return () => {
      // Cleanup event listener when component is destroyed
      window.removeEventListener("scroll", handleScroll);
    };
  });

  function myProfile(){
    let id = jwtDecode(localStorage.getItem("token"))["sub"];
    window.location.replace(`/profile/${id}`);
  }

</script>

<div
  class={`btm-nav transition-transform duration-300 transform ${
    isNavHidden ? "translate-y-full" : "translate-y-0"
  }`}
>
  <a href="/feed">
    <button
      class={$page.url.pathname === "/feed" ? "accent-button" : "text-primary"}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
        />
      </svg>
    </button>
  </a>

  <button
    class={($page.url.pathname == "/createImage") |
    ($page.url.pathname == "/createText")
      ? "accent-button"
      : "text-primary"}
    onclick="create_popup.showModal()"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="h-6 w-6"
      fill="currentColor"
      viewBox="0 0 24 24"
      stroke-width="0"
    >
      <path
        d="M12,1A11,11,0,1,0,23,12,11.013,11.013,0,0,0,12,1Zm0,20a9,9,0,1,1,9-9A9.01,9.01,0,0,1,12,21Zm5-9a1,1,0,0,1-1,1H13v3a1,1,0,0,1-2,0V13H8a1,1,0,0,1,0-2h3V8a1,1,0,0,1,2,0v3h3A1,1,0,0,1,17,12Z"
      />
    </svg>
  </button>

  <a>
    <button on:click={myProfile}>
      <div class="avatar">
        <div
          class="w-5 rounded-full ring ring-offset-base-100 {$page.url
            .pathname.includes('/profile')
            ? 'ring-accent'
            : 'ring-primary'} ring-offset-2"
        >
          <img
            src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp"
          />
        </div>
      </div>
    </button>
  </a>
</div>

<dialog id="create_popup" class="modal modal-bottom">
  <div class="modal-box">
    <div class="flex flex-col w-full border-opacity-50">
      <div class="grid h-10 card rounded-box place-items-center">
        <a href="/createText">
          <button
            class="btn btn-ghost text-2xl"
            on:click={() => create_popup.close()}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-7 w-7"
              fill="#ffffff"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="0"
            >
              <path
                d="M18,20H2c-0.6,0-1-0.4-1-1s0.4-1,1-1h16c0.6,0,1,0.4,1,1S18.6,20,18,20z"
              />
              <path
                d="M7,16H3c-0.6,0-1-0.4-1-1v-4c0-0.3,0.1-0.5,0.3-0.7l10-10c0.4-0.4,1-0.4,1.4,0l4,4c0.4,0.4,0.4,1,0,1.4l-10,10
					   C7.5,15.9,7.3,16,7,16z M4,14h2.6l9-9L13,2.4l-9,9V14z"
              />
            </svg> Text
          </button>
        </a>
      </div>
      <div class="divider text-xs">OR</div>
      <div class="grid h-10 card rounded-box place-items-center">
        <a href="/createImage">
          <button
            class="btn btn-ghost text-2xl"
            on:click={() => create_popup.close()}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-7 w-7"
              fill="#ffffff"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="0"
              ><circle cx="10" cy="11" r="4" />
              <path
                d="M19,19H1c-0.6,0-1-0.4-1-1V5c0-0.6,0.4-1,1-1h3.6l2.7-2.7C7.5,1.1,7.7,1,8,1h4c0.3,0,0.5,0.1,0.7,0.3L15.4,4H19
									c0.6,0,1,0.4,1,1v13C20,18.6,19.6,19,19,19z M2,17h16V6h-3c-0.3,0-0.5-0.1-0.7-0.3L11.6,3H8.4L5.7,5.7C5.5,5.9,5.3,6,5,6H2V17z"
              /></svg
            >
            Image
          </button></a
        >
      </div>
    </div>
  </div>

  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
