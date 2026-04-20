def somme_nulle_de_trois(tableau):
    tableau.sort() 
    result = []
    
    for i in range(len(tableau) - 2):  
        if i > 0 and tableau[i] == tableau[i - 1]:  
            continue
        
        left, right = i + 1, len(tableau) - 1 
        while left < right:
            total = tableau[i] + tableau[left] + tableau[right]  
            if total == 0:
                result.append((tableau[i], tableau[left], tableau[right]))  
                left += 1
                right -= 1
             
                while left < right and tableau[left] == tableau[left - 1]:
                    left += 1
                while left < right and tableau[right] == tableau[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1  
            else:
                right -= 1 
    
    return result

tableau = [1, -1, 0, 2, -2, 3, -3]
resultat = somme_nulle_de_trois(tableau)
print("Somme nulle de trois éléments:", resultat)  