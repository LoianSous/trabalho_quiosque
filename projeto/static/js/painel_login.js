document.addEventListener("DOMContentLoaded", () => {
  const toasts = document.querySelectorAll(".toast");

  toasts.forEach((toast) => {
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(-10px)";
      toast.style.transition = "opacity 0.4s ease, transform 0.4s ease";
      setTimeout(() => toast.remove(), 400);
    }, 4000);
  });
});