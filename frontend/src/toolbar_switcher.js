document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-link');
    const pages = document.querySelectorAll('.page');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            setActivePage(this.dataset.page);
        });
    });

    function setActivePage(pageName) {
        // Remove active class from all links and pages
        navLinks.forEach(link => link.classList.remove('active'));
        pages.forEach(page => page.classList.remove('active'));
    
        // Find the link and page corresponding to pageName
        const activeLink = [...navLinks].find(link => link.dataset.page === pageName);
        const activePage = document.getElementById(pageName);
    
        // Add active class to them
        if (activeLink) {
            activeLink.classList.add('active');
        }
        if (activePage) {
            activePage.classList.add('active');
        }
    
        // Scroll to the top of the page
        window.scrollTo(0, 0);
    }
    
    window.setActivePage = setActivePage;    
});
