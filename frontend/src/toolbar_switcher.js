document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-link');
    const pages = document.querySelectorAll('.page');
    const orderBonesHome = document.getElementById('home-order-now');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            setActivePage(this.dataset.page);
        });
    });

    function setActivePage(pageName) {
        // Remove active class from all links and pages
        navLinks.forEach(link => {
            link.classList.remove('active');
            // Diagnostic log
        });
        pages.forEach(page => page.classList.remove('active'));
    
        // Add active class to all links corresponding to pageName
        navLinks.forEach(link => {
            if (link.dataset.page === pageName) {
                link.classList.add('active');
                // Diagnostic log
            }
        });
    
        // Add active class to the page that corresponds to pageName
        const activePage = document.getElementById(pageName);
        if (activePage) {
            activePage.classList.add('active');
        }
    
        // Scroll to the top of the page
        window.scrollTo(0, 0);
    }
    // Allow this function to be accesible from anywhere.
    window.setActivePage = setActivePage;

    orderBonesHome.addEventListener('click', () => {
        setActivePage('order');
    });
});
