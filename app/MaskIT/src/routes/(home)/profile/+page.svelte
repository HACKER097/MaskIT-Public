<script>
    /** @type {import('./$types').PageData} */
    import { fade } from 'svelte/transition';
	import { slide } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
    export let data;

</script>

<div class="border-2 m-2 rounded-xl">
    <div class="divider mt-32 mb-28 ">
        <div class="w-96 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
            <div class="mask mask-circle ">
                <img src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
              </div>
        </div>
    </div>
    <h1 class="text-3xl text-center">Username</h1>
    <div class="stats shadow w-full stats-vertical sm:stats-horizontal">
  
        <div class="stat place-items-center">
          <div class="stat-title">Posts</div>
          <div class="stat-value">31</div>
          <div class="stat-desc">Since January 1st</div>
        </div>
        
        <div class="stat place-items-center">
          <div class="stat-title">Karma</div>
          <div class="stat-value text-secondary">4,200</div>
          <div class="stat-desc text-secondary">↗︎ 40 (2%)</div>
        </div>
        
        <div class="stat place-items-center">
          <div class="stat-title">Comments</div>
          <div class="stat-value">200</div>
          <div class="stat-desc">↘︎ 90 (14%)</div>
        </div>
        
      </div>
</div>


  <div class="content-center">
    {#each {length: 10} as _, i}
    <div class="card bg-base-100 mb-0 mt-5 border-0">
        <figure><img src="https://daisyui.com/images/stock/photo-1606107557195-0e29a4b5b4aa.jpg"  alt="Shoes" /></figure>
        <p class="p-2">Yoo, shoes are cool af frfr</p>
        <div class="card-body p-1">
          <div class="card-actions  ">
            <button class="btn btn-ghost btn-square m-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentcolor" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 14h4v7a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-7h4a1.001 1.001 0 0 0 .781-1.625l-8-10c-.381-.475-1.181-.475-1.562 0l-8 10A1.001 1.001 0 0 0 4 14z" /></svg>
            </button>
            <div class="btn btn-ghost btn-square text-xl">7</div>
            <button class="btn btn-ghost btn-square">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentcolor" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20.901 10.566A1.001 1.001 0 0 0 20 10h-4V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v7H4a1.001 1.001 0 0 0-.781 1.625l8 10a1 1 0 0 0 1.562 0l8-10c.24-.301.286-.712.12-1.059z" /></svg>
            </button>
            </div>
        </div>
      </div>

      <div class="divider m-0"></div> 

      <div class="card bg-base-100 mb-0 mt-0 border-0">
        <div class="m-5">
            <h1 class="card-title mb-5 text-3xl">Post title!</h1>
            <p class="mb-0 h-36 overflow-hidden [mask:linear-gradient(0deg,#0000,#000_1.25rem)] md:[mask:linear-gradient(0deg,#0000,#000_1.5rem)]">🌌 Embarked on an interdimensional escapade today and stumbled upon a cosmic realm where cats are not just adorable companions but linguistic maestros! 🐱🇫🇷 They speak French with the elegance of seasoned poets and, believe it or not, have a penchant for salsa dancing! 💃🕺 In this feline-inspired universe, yarn towers soar high, mirroring our iconic Eiffel Tower but with a playful twist.

                As I meandered through this alternate reality, I couldn't help but marvel at the cultural exchange happening between cats and humans. Imagine sipping espresso at a Parisian café, engaging in profound conversations with your sophisticated kitty companion who critiques the latest catnip-infused poetry. 📜☕️
                
                Meanwhile, back in our reality, my coffee mug seems to be harboring secrets – is it secretly plotting against me, or am I just experiencing a caffeine-induced conspiracy theory? ☕️🤔
                
                Have you ever daydreamed about a world where the ordinary becomes extraordinary? Share your whimsical thoughts and let's unravel the tapestry of our collective imagination! ✨🌈 #ParallelUniverseAdventures #CatsSpeakFrench #YarnTowerWonders"</p>
        </div>
        <div class="card-body p-1">
          <div class="card-actions  ">
            <button class="btn btn-ghost btn-square">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentcolor" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 14h4v7a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-7h4a1.001 1.001 0 0 0 .781-1.625l-8-10c-.381-.475-1.181-.475-1.562 0l-8 10A1.001 1.001 0 0 0 4 14z" /></svg>
            </button>
            <div class="btn btn-ghost btn-square text-xl">7</div>
            <button class="btn btn-ghost btn-square">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentcolor" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20.901 10.566A1.001 1.001 0 0 0 20 10h-4V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v7H4a1.001 1.001 0 0 0-.781 1.625l8 10a1 1 0 0 0 1.562 0l8-10c.24-.301.286-.712.12-1.059z" /></svg>
            </button>
            </div>
        </div>

        <div class="divider m-0"></div> 
      </div>

      {/each}
</div>

