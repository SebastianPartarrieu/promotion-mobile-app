function sendSearchRequest(search,categorie,updateFunction,route){

    const url = new URL(route, server.server)
  
    const recherche = search;
    url.searchParams.append('search',recherche)
    if (categorie!='')
      { 
        url.searchParams.append('categorie',categorie)
      };
    
  
    fetch(url, {
      method : 'GET',
      headers: {
        Accept: 'application/json',},
  
    }).then((response) => response.json()).then(updateFunction).catch(
      (e) => {alert('Something went wrong' + e.message)}
    )
  }