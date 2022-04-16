document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            // e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

    const categories = document.querySelectorAll('#category');
    const institutions = document.querySelectorAll('#institution');
    let selected_categories = [];
    categories.forEach(function (category) {
        category.addEventListener('change', function () {
            if (this.checked) {
                selected_categories.push(category.value);
            } else {
                let ind = selected_categories.indexOf(category.value);
                selected_categories.splice(ind, 1);
            }
            institutions.forEach(function (institution) {
                let institution_categories = Array.from(institution.firstElementChild.firstElementChild.children).map(function (element) {
                    return element.value;
                })
                if (selected_categories.length !== 0 && selected_categories.every(i => institution_categories.includes(i))) {
                    institution.removeAttribute('hidden');
                } else {
                    institution.setAttribute('hidden', true);
                }
            });
        })
    });
    const summary_button = document.querySelector('#summary');
    const bags = document.querySelector('#bags');
    const foundation = document.querySelector('#foundation');
    const street = document.querySelector('#street');
    const city = document.querySelector('#city');
    const code = document.querySelector('#code');
    const phone = document.querySelector('#phone');
    const date = document.querySelector('#date');
    const time = document.querySelector('#time');
    const comment = document.querySelector('#comment');
    const institutions_inputs = document.querySelectorAll('#institutioninput')
    let selected_institution = ''
    summary_button.addEventListener('click', function () {
        let cat_text = '';
        categories.forEach(function (category) {
            if (category.checked) {
                cat_text += category.nextElementSibling.nextElementSibling.innerText + ', ';
            }
        })
        let bags_input = document.querySelector('#bagsinput').value
        let bags_word = ''
        if (bags_input == 1) {
            bags_word = ' worek '
        } else if ((bags_input % 10 == 2 || bags_input % 10 == 3 || bags_input % 10 == 4) && (bags_input < 10 || bags_input > 20)) {
            bags_word = ' worki '
        } else {
            bags_word = ' worków '
        }
        bags.innerText = bags_input + bags_word + cat_text;
        institutions_inputs.forEach(function (institution_input) {
            if (institution_input.checked) {
                selected_institution = institution_input.nextElementSibling.nextElementSibling.firstElementChild.innerText
            }
        })
        foundation.innerText = 'Dla ' + selected_institution
        street.innerText = document.querySelector('#streetinput').value;
        city.innerText = document.querySelector('#cityinput').value;
        code.innerText = document.querySelector('#codeinput').value;
        phone.innerText = document.querySelector('#phoneinput').value;
        date.innerText = document.querySelector('#dateinput').value;
        time.innerText = document.querySelector('#timeinput').value;
        if (document.querySelector('#commentinput').value === '') {
            comment.innerText = 'Brak uwag'
        } else {
            comment.innerText = document.querySelector('#commentinput').value;
        }
    })
});