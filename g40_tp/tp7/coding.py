def fusionner_tableaux(nums1, nums2):
    i = 0
    j = 0
    resultat = []

    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            resultat.append(nums1[i])
            i += 1
        else:
            resultat.append(nums2[j])
            j += 1

    while i < len(nums1):
        resultat.append(nums1[i])
        i += 1

    while j < len(nums2):
        resultat.append(nums2[j])
        j += 1

    return resultat


print(fusionner_tableaux([1, 2, 3], [2, 5, 6]))
print(fusionner_tableaux([1], []))