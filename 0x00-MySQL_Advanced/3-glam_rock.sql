-- SQL script that lists all bands with Glam rock as main style, ranked by longevity
SELECT band_name, COALESCE(split, 2022) - formed AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
