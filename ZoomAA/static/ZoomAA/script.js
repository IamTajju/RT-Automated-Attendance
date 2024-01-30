const form = document.getElementById("new_document_attachment");
const fileInput = document.getElementById("document_attachment_doc");
const fileInput2 = document.getElementById("document_attachment_doc2");
const fileInput3 = document.getElementById("document_attachment_doc3");

window.addEventListener('paste', e => {
    fileInput.files = e.clipboardData.files;
    window.addEventListener('paste', e => {
        fileInput2.files = e.clipboardData.files;
        window.addEventListener('paste', e => {
            fileInput3.files = e.clipboardData.files;

        });
    });
});
