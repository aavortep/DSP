function lab_09()
    I=double(imread('bimage5.bmp')) / 255;

    figure;
    imshow(I);
    title('Source image');

    PSF=fspecial('motion', 40, 30);
    [J1, ~]=deconvblind(I, PSF);
    figure;
    imshow(J1);
    title('Recovered image');
end
