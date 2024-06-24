document.addEventListener('DOMContentLoaded', function() {
  const filterButtons = document.getElementById('filter-buttons');
  const prendasList = Array.from(document.getElementsByClassName('prenda-item'));
  const noPrendasMessage = document.createElement('div');
  noPrendasMessage.className = 'col-md-12';
  noPrendasMessage.innerHTML = '<p class="text-center">No ha subido ninguna prenda de esta categoria.</p>';
  
  filterButtons.addEventListener('change', function(event) {
    const selectedCategory = event.target.value;
    let visibleCount = 0;
    
    prendasList.forEach(prenda => {
      if (selectedCategory === 'Todos' || prenda.dataset.category === selectedCategory) {
        prenda.style.display = 'flex';
        visibleCount++;
      } else {
        prenda.style.display = 'none';
      }
    });
    
    const prendasListContainer = document.getElementById('prendas-list');
    
    if (visibleCount === 0) {
      if (!document.getElementById('no-prendas-message')) {
        noPrendasMessage.id = 'no-prendas-message';
        prendasListContainer.appendChild(noPrendasMessage);
      }
    } else {
      const existingMessage = document.getElementById('no-prendas-message');
      if (existingMessage) {
        existingMessage.remove();
      }
    }
  });
});
