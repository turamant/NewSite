// Получаем ссылку на иконку комментариев
const commentIcon = document.querySelectorAll('.comment-icon');

// Получаем ссылку на модальное окно
const modal = document.getElementById('commentModal');
const modalContent = modal.querySelector('.rounded-lg');

// Флаг для отслеживания состояния модального окна
let isModalOpen = false;

// Добавляем обработчики событий
commentIcon.forEach(icon => {
    icon.addEventListener('click', () => {
        if (!isModalOpen) {
            // Здесь вы можете сделать запрос на сервер, чтобы получить комментарии
            // и отобразить их в модальном окне
            const postId = icon.dataset.postId;
            fetchComments(postId);
            showModal();
            isModalOpen = true;
        }
    });
});

modalContent.addEventListener('mouseleave', () => {
    if (isModalOpen) {
        hideModal();
        isModalOpen = false;
    }
});

// Функция для отображения модального окна
function showModal() {
    modal.classList.remove('opacity-0', 'scale-90', 'invisible');
    centerModal();
}

// Функция для скрытия модального окна
function hideModal() {
    modal.classList.add('opacity-0', 'scale-90', 'invisible');
}

// Функция для центрирования модального окна
function centerModal() {
    const modalHeight = modal.offsetHeight;
    const windowHeight = window.innerHeight;
    const top = (windowHeight - modalHeight) / 2 + 50; // Опустить на 50 пикселей
    modal.style.top = `${top}px`;
}

// Функция для получения комментариев с сервера
function fetchComments(postId) {
    fetch(`/posts/${postId}/comments/`)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error fetching comments');
            }
        })
        .then(data => {
            const commentList = document.getElementById('commentList');
            commentList.innerHTML = '';

            if (data.length === 0) {
                commentList.innerHTML = '<p>Комментариев пока нет</p>';
            } else {
                data.forEach((comment, index) => {
                    const commentElement = document.createElement('div');
                    commentElement.classList.add('mb-4');
                    commentElement.innerHTML = `
                        <p class="font-bold">Комментарий #${index + 1}</p>
                        <p>${comment.content}</p>
                    `;
                    commentList.appendChild(commentElement);
                });
            }
        })
        .catch(error => {
            const commentList = document.getElementById('commentList');
            commentList.innerHTML = `<p class="text-red-500">${error.message}</p>`;
            console.error('Error fetching comments:', error);
        });
}
