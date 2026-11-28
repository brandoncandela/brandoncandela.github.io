// Tour videos play only for visitors who allow motion, and only once they scroll near them.
// The markup has no autoplay attribute, so reduced-motion visitors (and visitors without
// JavaScript) see the poster image and the video never downloads.
(() => {
  const videos = document.querySelectorAll("video[data-autoplay]");
  if (!videos.length) return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  const start = (video) => {
    if (reduce.matches) return;
    video.muted = true;
    video.play().catch(() => {});
  };
  if ("IntersectionObserver" in window) {
    const seen = new IntersectionObserver((entries) => {
      entries.forEach((entry) => (entry.isIntersecting ? start(entry.target) : entry.target.pause()));
    }, { rootMargin: "200px 0px" });
    videos.forEach((video) => seen.observe(video));
  } else {
    videos.forEach(start);
  }
  reduce.addEventListener("change", () => {
    videos.forEach((video) => (reduce.matches ? video.pause() : start(video)));
  });
})();
