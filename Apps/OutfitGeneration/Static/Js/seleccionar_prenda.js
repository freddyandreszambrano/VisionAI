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
    
    
});