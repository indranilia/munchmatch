const btn = document.querySelector("button");
const post = document.querySelector(".post");
const review = document.querySelector(".review");
const edit = document.querySelector(".edit");

/* the detailed comment widget shows only after the hearts are clicked */
/* the edit button shows after the review is submitted */

btn.onclick = () => {
    review.style.display = "none";
    post.style.display = "block";
    edit.onclick = () => {
        review.style.display = "block";
        post.style.display = "none";
    }
    return false;
}
