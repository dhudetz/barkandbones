document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-link');
    const pages = document.querySelectorAll('.page');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            // Remove active class from all links and pages
            navLinks.forEach(link => link.classList.remove('active'));
            pages.forEach(page => page.classList.remove('active'));

            // Add active class to clicked link and corresponding page
            this.classList.add('active');
            const pageId = this.dataset.page;
            document.getElementById(pageId).classList.add('active');
        });
    });
});
