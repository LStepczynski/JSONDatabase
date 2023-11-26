let lastChild;
let lastChildInputs;

const doc_creator = document.getElementById("document-creator")

const monitor = (inputs) => {
    const checkInputsHandler = () => {
        checkInputs();
    };

    inputs.forEach(input => {
        input.addEventListener('input', checkInputsHandler);
    });
};

const checkInputs = () => {
    const [key, value] = lastChildInputs;

    if (key.value !== "" && value.value !== "") {
        lastChildInputs.forEach(input => {
            input.removeEventListener('input', checkInputs);
        });

        const newPairElement = document.createElement('div');
        const keyParagraph = document.createElement('p');
        keyParagraph.textContent = "Key";
        const keyInput = document.createElement('input');
        keyInput.name = "key";

        const valueParagraph = document.createElement('p');
        valueParagraph.textContent = "Value";
        const valueInput = document.createElement('input');
        valueInput.name = "value";

        newPairElement.appendChild(keyParagraph);
        newPairElement.appendChild(keyInput);
        newPairElement.appendChild(valueParagraph);
        newPairElement.appendChild(valueInput);

        doc_creator.appendChild(newPairElement);
        newPair();
    }
};

const newPair = () => {
    lastChild = doc_creator.lastElementChild;
    lastChildInputs = Array.from(lastChild.querySelectorAll('input'));
    monitor(lastChildInputs);
};

// Initial call to create the first set of inputs
newPair();
