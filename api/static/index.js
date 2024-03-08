function deleteNote(noteId) { // note.id is passed into the function
    fetch('/delete-note', {
        method: 'POST', // sends a POST request to "/delete-note" endpoint
        body: JSON.stringify({ noteId: noteId }) // creates a json formatted string
    }).then((_res) => {
        window.location.href = "/";
    });
};

const sortableList = document.querySelector(".list-group");
const items = document.querySelectorAll(".list-group-item");

items.forEach(item => {
    item.addEventListener("dragstart", () => {
        // Adding dragging class to item after a delay
        setTimeout(() => item.classList.add("dragging"), 0);
    });
    item.addEventListener("dragend", () => {
        // Removing dragging class from item on dragend event
        item.classList.remove("dragging");
        sortDatabase();
    });
});

function initSortableList(e) {
    e.preventDefault()

    const draggingItem = sortableList.querySelector(".dragging");

    // Getting all items except currently dragging and making array of them
    const siblings = [...sortableList.querySelectorAll(".list-group-item:not(.dragging)")];

    // Finding the sibling after which the dragging item should be placed
    let nextSibling = siblings.find(sibling => {
        return e.clientY <= sibling.offsetTop + sibling.offsetHeight / 2;
    });

    // Inserting the dragging item before the found sibling
    sortableList.insertBefore(draggingItem, nextSibling);
};

function sortDatabase() {
    const items = document.querySelectorAll(".list-group-item");

    var noteIds = []
    items.forEach(item => {
        noteIds.push(item.getAttribute("id"))
    });

    fetch('/sort-database', {
        method: 'POST',
        body: JSON.stringify({ note_ids: noteIds })
    });
};

sortableList.addEventListener("dragover", initSortableList);