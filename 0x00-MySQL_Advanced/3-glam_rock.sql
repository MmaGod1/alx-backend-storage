-- List Glam Rock bands ranked by their longevity
SELECT 
    band_name,
    CASE 
        WHEN split IS NOT NULL THEN split - formed
        ELSE 2022 - formed 
    END AS lifespan
FROM 
    metal_bands
WHERE 
    style LIKE '%Glam rock%'
ORDER BY 
    lifespan DESC;
