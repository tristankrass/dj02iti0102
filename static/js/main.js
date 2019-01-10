const burger = document.querySelector("#navBurger");

const navbar_content = document.querySelector("#mainNavbar");

burger.addEventListener("click", function () {
    navbar_content.classList.toggle("is-active");
    burger.classList.toggle("is-active");
});

const replyField = document.querySelector("#replyToComment");

const commentReplyBtn = document.querySelector("#replyButton");

commentReplyBtn.addEventListener("click", function () {
    replyField.classList.toggle("is-hidden");
});
