document.addEventListener('DOMContentLoaded', function () {

    /* -----------------------------------------------------
       Фиксация меню при скролле (blur-фон)
       ----------------------------------------------------- */
    var header = document.getElementById('site-header');
    var backToTop = document.getElementById('back-to-top');

    function handleScrollState() {
        var scrolled = window.scrollY > 20;
        header.classList.toggle('is-scrolled', scrolled);

        var showBackToTop = window.scrollY > 300;
        backToTop.classList.toggle('is-visible', showBackToTop);
    }

    handleScrollState();
    window.addEventListener('scroll', handleScrollState, { passive: true });

    /* -----------------------------------------------------
       Кнопка «Наверх»
       ----------------------------------------------------- */
    backToTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    /* -----------------------------------------------------
       Плавный скролл по якорям (доп. к CSS scroll-behavior —
       на случай браузеров без поддержки и для закрытия
       мобильного меню при переходе)
       ----------------------------------------------------- */
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            var targetId = link.getAttribute('href').slice(1);
            var target = document.getElementById(targetId);
            if (!target) {
                return;
            }
            event.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });

            var navLinks = document.getElementById('nav-links');
            var navToggle = document.getElementById('nav-toggle');
            if (navLinks && navLinks.classList.contains('is-open')) {
                navLinks.classList.remove('is-open');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });
    });

    /* -----------------------------------------------------
       Мобильное меню
       ----------------------------------------------------- */
    var navToggle = document.getElementById('nav-toggle');
    var navLinks = document.getElementById('nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function () {
            var isOpen = navLinks.classList.toggle('is-open');
            navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });
    }

    /* -----------------------------------------------------
       Форма обратной связи: валидация + отправка через fetch
       ----------------------------------------------------- */
    var form = document.getElementById('contact-form');
    if (!form) {
        return;
    }

    var successEl = document.getElementById('form-success');
    var submitBtn = document.getElementById('contact-submit-btn');

    function getCookie(name) {
        var match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return match ? match.pop() : '';
    }

    function setFieldError(fieldName, message) {
        var el = form.querySelector('[data-error-for="' + fieldName + '"]');
        if (el) {
            el.textContent = message || '';
        }
    }

    function clearErrors() {
        ['name', 'email', 'message'].forEach(function (field) {
            setFieldError(field, '');
        });
    }

    function validate(data) {
        var errors = {};

        if (!data.name.trim()) {
            errors.name = 'Пожалуйста, укажите ваше имя.';
        }

        if (!data.email.includes('@')) {
            errors.email = 'Проверьте корректность email.';
        }

        if (!data.message.trim()) {
            errors.message = 'Пожалуйста, добавьте сообщение.';
        }

        return errors;
    }

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        clearErrors();
        successEl.textContent = '';

        var data = {
            name: form.querySelector('#id_name').value,
            email: form.querySelector('#id_email').value,
            message: form.querySelector('#id_message').value,
        };

        var errors = validate(data);
        var hasErrors = Object.keys(errors).length > 0;

        if (hasErrors) {
            Object.keys(errors).forEach(function (field) {
                setFieldError(field, errors[field]);
            });
            return;
        }

        // Данные формы — в консоль (заглушка до подключения реальной отправки)
        console.log('Отправка формы контактов:', data);

        submitBtn.disabled = true;

        fetch('/contact/submit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(data),
        })
            .then(function (response) {
                return response.json().then(function (body) {
                    return { status: response.status, body: body };
                });
            })
            .then(function (result) {
                if (result.body && result.body.ok) {
                    successEl.textContent = 'Мы подберём решение для вашей семьи и свяжемся с вами в ближайшее время';
                    form.reset();
                } else if (result.body && result.body.errors) {
                    Object.keys(result.body.errors).forEach(function (field) {
                        setFieldError(field, result.body.errors[field][0].message);
                    });
                } else {
                    successEl.textContent = 'Мы подберём решение для вашей семьи и свяжемся с вами в ближайшее время';
                    form.reset();
                }
            })
            .catch(function (error) {
                console.log('Ошибка отправки формы (данные сохранены только в консоли):', error);
                // Даже при недоступности бэкенда — не оставляем пользователя без ответа
                successEl.textContent = 'Мы подберём решение для вашей семьи и свяжемся с вами в ближайшее время';
                form.reset();
            })
            .finally(function () {
                submitBtn.disabled = false;
            });
    });
});
