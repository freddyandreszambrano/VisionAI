document.addEventListener("DOMContentLoaded", function() {
    const selectedItems = {
        inferior: null,
        zapatos: null,
        superior: null
    };
    const carousels = [
        {id: '#carouselPrendasInferiores', type: 'inferior'},
        {id: '#carouselZapatos', type: 'zapatos'},
        {id: '#carouselPrendasSuperiores', type: 'superior'}
    ];

    carousels.forEach(carousel => {
        const carouselElement = document.querySelector(carousel.id);
        const images = carouselElement.querySelectorAll(`.selector-circle[data-type="${carousel.type}"]`);

        images.forEach(image => {
            image.addEventListener('click', function() {
                const isActive = this.classList.contains('active');

                images.forEach(selector => {
                    selector.classList.remove('active');
                });

                if (!isActive) {
                    this.classList.add('active');

                    const bootstrapCarousel = bootstrap.Carousel.getInstance(carouselElement);
                    if (bootstrapCarousel) {
                        bootstrapCarousel.pause();
                    }

                    const img = this.previousElementSibling;
                    const [id, category] = img.alt.split(',');

                    selectedItems[carousel.type] = {
                        id: id.trim(),
                        category: category.trim()
                    };

                } else {
                    const bootstrapCarousel = bootstrap.Carousel.getInstance(carouselElement);
                    if (bootstrapCarousel) {
                        bootstrapCarousel.cycle();
                    }
                    selectedItems[carousel.type] = null;
                }
            });
        });
    });
    
     // Send selected items to the server
     document.querySelector("#sendSelectionButton").addEventListener("click", function() {
        fetch("{% url 'OutfitGeneration:process_selection' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify(selectedItems)
        })
        .then(response => response.json())
        .then(data => {
            window.location.href = "{% url 'OutfitGeneration:show_selection' %}";
        })
        .catch(error => console.error("Error:", error));
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});