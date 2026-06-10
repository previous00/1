const API_BASE = 'http://localhost:5000/api';

const { createApp, ref, computed, onMounted, watch } = Vue;

createApp({
    setup() {
        const currentUser = ref(null);
        const token = ref(localStorage.getItem('token') || '');
        const authMode = ref('login');
        const authForm = ref({ username: '', password: '' });
        const authError = ref('');
        const currentView = ref('books');
        const message = ref('');
        const messageType = ref('success');

        // Books
        const books = ref([]);
        const bookPage = ref(1);
        const bookPages = ref(0);
        const searchKeyword = ref('');
        const searchCategory = ref('');
        const categories = ref([]);
        const showDetail = ref(false);
        const detailBook = ref({});

        // Admin books
        const adminBooks = ref([]);
        const adminBookPage = ref(1);
        const adminBookPages = ref(0);
        const showBookForm = ref(false);
        const editingBook = ref(null);
        const bookForm = ref({
            title: '', author: '', isbn: '', publisher: '',
            publish_date: '', category_id: null, total_count: 1, description: ''
        });

        // Categories
        const newCategoryName = ref('');
        const editingCategory = ref(null);
        const editCategoryName = ref('');

        // Borrows
        const borrowRecords = ref([]);
        const borrowPage = ref(1);
        const borrowPages = ref(0);
        const allBorrowRecords = ref([]);
        const allBorrowPage = ref(1);
        const allBorrowPages = ref(0);

        const isAdmin = computed(() => currentUser.value && currentUser.value.role === 'admin');

        function headers() {
            return {
                'Content-Type': 'application/json',
                'Authorization': token.value ? `Bearer ${token.value}` : ''
            };
        }

        function showMessage(msg, type = 'success') {
            message.value = msg;
            messageType.value = type;
            setTimeout(() => { message.value = ''; }, 3000);
        }

        function formatDate(dateStr) {
            if (!dateStr) return '-';
            return new Date(dateStr).toLocaleString('zh-CN');
        }

        // Auth
        async function handleAuth() {
            authError.value = '';
            const url = authMode.value === 'login' ? '/auth/login' : '/auth/register';
            try {
                const res = await fetch(API_BASE + url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(authForm.value)
                });
                const data = await res.json();
                if (!res.ok) {
                    authError.value = data.message;
                    return;
                }
                if (authMode.value === 'register') {
                    authMode.value = 'login';
                    showMessage('注册成功，请登录');
                    return;
                }
                token.value = data.token;
                localStorage.setItem('token', data.token);
                currentUser.value = data.user;
                loadCategories();
                loadBooks();
            } catch (e) {
                authError.value = '网络错误，请确认后端服务已启动';
            }
        }

        function logout() {
            token.value = '';
            currentUser.value = null;
            localStorage.removeItem('token');
            authForm.value = { username: '', password: '' };
        }

        // Books
        async function loadBooks() {
            const params = new URLSearchParams({
                page: bookPage.value,
                per_page: 9,
                keyword: searchKeyword.value,
            });
            if (searchCategory.value) params.append('category_id', searchCategory.value);
            try {
                const res = await fetch(`${API_BASE}/books?${params}`);
                const data = await res.json();
                books.value = data.books;
                bookPages.value = data.pages;
            } catch (e) {
                showMessage('加载图书失败', 'error');
            }
        }

        function searchBooks() {
            bookPage.value = 1;
            loadBooks();
        }

        function changePage(p) {
            bookPage.value = p;
            loadBooks();
        }

        function viewBookDetail(book) {
            detailBook.value = book;
            showDetail.value = true;
        }

        async function borrowBook(bookId) {
            try {
                const res = await fetch(`${API_BASE}/borrows`, {
                    method: 'POST',
                    headers: headers(),
                    body: JSON.stringify({ book_id: bookId })
                });
                const data = await res.json();
                if (!res.ok) {
                    showMessage(data.message, 'error');
                    return;
                }
                showMessage('借阅成功');
                loadBooks();
            } catch (e) {
                showMessage('操作失败', 'error');
            }
        }

        // Admin books
        async function loadAdminBooks() {
            const params = new URLSearchParams({ page: adminBookPage.value, per_page: 10 });
            try {
                const res = await fetch(`${API_BASE}/books?${params}`);
                const data = await res.json();
                adminBooks.value = data.books;
                adminBookPages.value = data.pages;
            } catch (e) {
                showMessage('加载图书失败', 'error');
            }
        }

        function changeAdminBookPage(p) {
            adminBookPage.value = p;
            loadAdminBooks();
        }

        function openBookForm(book) {
            editingBook.value = book;
            if (book) {
                bookForm.value = { ...book };
            } else {
                bookForm.value = {
                    title: '', author: '', isbn: '', publisher: '',
                    publish_date: '', category_id: null, total_count: 1, description: ''
                };
            }
            showBookForm.value = true;
        }

        async function saveBook() {
            const url = editingBook.value
                ? `${API_BASE}/books/${editingBook.value.id}`
                : `${API_BASE}/books`;
            const method = editingBook.value ? 'PUT' : 'POST';
            try {
                const res = await fetch(url, {
                    method,
                    headers: headers(),
                    body: JSON.stringify(bookForm.value)
                });
                const data = await res.json();
                if (!res.ok) {
                    showMessage(data.message, 'error');
                    return;
                }
                showMessage(editingBook.value ? '修改成功' : '添加成功');
                showBookForm.value = false;
                loadAdminBooks();
                loadBooks();
            } catch (e) {
                showMessage('操作失败', 'error');
            }
        }

        async function deleteBook(bookId) {
            if (!confirm('确定要删除该图书吗？')) return;
            try {
                const res = await fetch(`${API_BASE}/books/${bookId}`, {
                    method: 'DELETE',
                    headers: headers()
                });
                const data = await res.json();
                if (!res.ok) {
                    showMessage(data.message, 'error');
                    return;
                }
                showMessage('删除成功');
                loadAdminBooks();
                loadBooks();
            } catch (e) {
                showMessage('操作失败', 'error');
            }
        }

        // Categories
        async function loadCategories() {
            try {
                const res = await fetch(`${API_BASE}/categories`);
                categories.value = await res.json();
            } catch (e) {}
        }

        async function addCategory() {
            if (!newCategoryName.value.trim()) return;
            try {
                const res = await fetch(`${API_BASE}/categories`, {
                    method: 'POST',
                    headers: headers(),
                    body: JSON.stringify({ name: newCategoryName.value.trim() })
                });
                const data = await res.json();
                if (!res.ok) {
                    showMessage(data.message, 'error');
                    return;
                }
                showMessage('添加成功');
                newCategoryName.value = '';
                loadCategories();
            } catch (e) {
                showMessage('操作失败', 'error');
            }
        }

        function startEditCategory(c) {
            editingCategory.value = c.id;
            editCategoryName.value = c.name;
        }

        async function updateCategory(id) {
            try {
                const res = await fetch(`${API_BASE}/categories/${id}`, {
                    method: 'PUT',
                    headers: headers(),
                    body: JSON.stringify({ name: editCategoryName.value.trim() })
                });
                const data = await res.json();
                if (!res.ok) {
                    showMessage(data.message, 'error');
                    return;
                }
                showMessage('修改成功');
                editingCategory.value = null;
                loadCategories();
            } catch (e) {
                showMessage('操作失败', 'error');
            }
        }

        async function deleteCategory(id) {
            if (!confirm('确定要删除该分类吗？')) return;
            try {
                const res = await fetch(`${API_BASE}/categories/${id}`, {
                    method: 'DELETE',
                    headers: headers()
                });
                const data = await res.json();
                if (!res.ok) {
                    showMessage(data.message, 'error');
                    return;
                }
                showMessage('删除成功');
                loadCategories();
            } catch (e) {
                showMessage('操作失败', 'error');
            }
        }

        // Borrows
        async function loadBorrowRecords() {
            const params = new URLSearchParams({ page: borrowPage.value, per_page: 10 });
            try {
                const res = await fetch(`${API_BASE}/borrows?${params}`, { headers: headers() });
                const data = await res.json();
                borrowRecords.value = data.records;
                borrowPages.value = data.pages;
            } catch (e) {}
        }

        function changeBorrowPage(p) {
            borrowPage.value = p;
            loadBorrowRecords();
        }

        async function loadAllBorrowRecords() {
            const params = new URLSearchParams({ page: allBorrowPage.value, per_page: 10 });
            try {
                const res = await fetch(`${API_BASE}/borrows?${params}`, { headers: headers() });
                const data = await res.json();
                allBorrowRecords.value = data.records;
                allBorrowPages.value = data.pages;
            } catch (e) {}
        }

        function changeAllBorrowPage(p) {
            allBorrowPage.value = p;
            loadAllBorrowRecords();
        }

        async function returnBook(recordId) {
            try {
                const res = await fetch(`${API_BASE}/borrows/${recordId}/return`, {
                    method: 'POST',
                    headers: headers()
                });
                const data = await res.json();
                if (!res.ok) {
                    showMessage(data.message, 'error');
                    return;
                }
                showMessage('归还成功');
                loadAllBorrowRecords();
                loadBooks();
            } catch (e) {
                showMessage('操作失败', 'error');
            }
        }

        // View watchers
        watch(currentView, (view) => {
            if (view === 'books') loadBooks();
            if (view === 'myBorrows') loadBorrowRecords();
            if (view === 'manageBooks') loadAdminBooks();
            if (view === 'manageCategories') loadCategories();
            if (view === 'manageBorrows') loadAllBorrowRecords();
        });

        // Init
        onMounted(async () => {
            if (token.value) {
                try {
                    const res = await fetch(`${API_BASE}/auth/me`, { headers: headers() });
                    if (res.ok) {
                        currentUser.value = await res.json();
                        loadCategories();
                        loadBooks();
                    } else {
                        localStorage.removeItem('token');
                        token.value = '';
                    }
                } catch (e) {
                    localStorage.removeItem('token');
                    token.value = '';
                }
            }
        });

        return {
            currentUser, authMode, authForm, authError, currentView,
            message, messageType, isAdmin,
            books, bookPage, bookPages, searchKeyword, searchCategory,
            categories, showDetail, detailBook,
            adminBooks, adminBookPage, adminBookPages,
            showBookForm, editingBook, bookForm,
            newCategoryName, editingCategory, editCategoryName,
            borrowRecords, borrowPage, borrowPages,
            allBorrowRecords, allBorrowPage, allBorrowPages,
            handleAuth, logout, formatDate,
            loadBooks, searchBooks, changePage, viewBookDetail, borrowBook,
            loadAdminBooks, changeAdminBookPage, openBookForm, saveBook, deleteBook,
            addCategory, startEditCategory, updateCategory, deleteCategory,
            changeBorrowPage, changeAllBorrowPage, returnBook,
            showMessage
        };
    }
}).mount('#app');
