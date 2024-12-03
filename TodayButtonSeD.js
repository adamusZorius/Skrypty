// ==UserScript==
// @name         Today Button
// @namespace    http://tampermonkey.net/
// @version      2024-11-04
// @description  Adding today button to SeD work time
// @author       Kacper Adamus
// @match        https://*.edokumenty.symfonia.pl/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=symfonia.pl
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    let date
    let alreadyAdded = []
    let startInput, endInput, dialogTodo

    const button = document.createElement('button')
    button.className = "rbos-btn rbos-btn-tertiary rbos-btn-cancel";
    button.style.cursor = "pointer"
    button.innerHTML = "Dzisiaj"

    button.onclick = (e) => {
        e.preventDefault()
        const today = new Date()
        date = today.getFullYear() + '-' + (today.getMonth()+1 < 10 ? "0" + today.getMonth()+1 : today.getMonth()+1) + '-' + (today.getDate() < 10 ? "0" + today.getDate() : today.getDate())
        startInput.value = date
        endInput.value = date
    }

    let currentId = ""
    let cActId = ""

    const addButton = (id) => {
        const element = document.querySelector("#"+id+"bpanel");

        if (id.includes("RCP")) {
            element.prepend(button)
            alreadyAdded.push(dialogTodo)
        }

        startInput = document.querySelector("#"+id+"rlstrtd")
        endInput = document.querySelector("#"+id+"rlend_d")


        const today = new Date()
        date = today.getFullYear() + '-' + (today.getMonth()+1 < 10 ? "0" + today.getMonth()+1 : today.getMonth()+1) + '-' + (today.getDate() < 10 ? "0" + today.getDate() : today.getDate())
        startInput.value = date
        endInput.value = date
    }

    const observer = new MutationObserver((mutations) => {
        mutations.forEach(mutation => {
            mutation.removedNodes.forEach(node => {
                if (node.nodeType === 1 && node.classList.contains('c-act')) {
                    alreadyAdded = [];
                }
            });
        });

        const dialogs = document.querySelectorAll(".Dialog")
        const cAct = document.querySelectorAll(".c-act")

        dialogs.forEach(dialog => dialog.removeEventListener("click", dialogListener))
        cAct.forEach(item => item.removeEventListener("click", cActListener))

        dialogs.forEach(dialog => dialogListener(dialog))
        cAct.forEach(item => cActListener(item))

        cAct.forEach(item => {
            cActId = item.attributes.edappref.value
            if (!alreadyAdded.includes(dialogTodo) && cActId.includes("RCP")) {
                addButton(cActId)
            }
        })
    })

    const dialogListener = (dialog) => {
        dialog.onclick = () => {
            currentId = dialog.attributes.id.value

            if (currentId.includes("TODOdlg")) {
                dialogTodo = currentId
            }
        }
    }

    const cActListener = (item) => {
        cActId = item.attributes.edappref.value
        if (cActId === currentId && !alreadyAdded.includes(dialogTodo) && cActId.includes("RCP")) {
            addButton(cActId)
        }
    }

    observer.observe(document.body, {
        childList: true,
        subtree: true
    })
})();

