// Add your js here
burger = document.querySelector("#navBurger");
navbar_content = document.querySelector("#mainNavbar");
burger.addEventListener("click", function () {
    navbar_content.classList.toggle("is-active");
    burger.classList.toggle("is-active");
});
var commentReplyBtn = document.querySelector("#replyButton");
var commentReplyArea = document.querySelector("#replyComment");
var createContentBtn = document.querySelector("#addContent");

commentReplyBtn.addEventListener("click", function () {
    commentReplyArea.classList.remove("is-hidden");
    commentReplyBtn.classList.add("is-hidden");
});
