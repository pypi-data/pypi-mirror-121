import SimpleITK as sitk
import pickle as pkl

def resampleImage(Image, SpacingScale = None, NewSpacing = None, NewSize = None, Interpolator=sitk.sitkLinear):
    Size = Image.GetSize()
    Spacing = Image.GetSpacing()
    Origin = Image.GetOrigin()
    Direction = Image.GetDirection()

    if not SpacingScale is None and NewSpacing is None and NewSize is None:
        NewSize = [int(Size[0]/SpacingScale),
                   int(Size[1]/SpacingScale),
                   int(Size[2]/SpacingScale)]
        NewSpacing = [Spacing[0]*SpacingScale,
                      Spacing[1]*SpacingScale,
                      Spacing[2]*SpacingScale]
    elif not NewSpacing is None and SpacingScale is None and NewSize is None:
        NewSize = [int(Size[0] * Spacing[0] / NewSpacing[0]),
                   int(Size[1] * Spacing[1] / NewSpacing[1]),
                   int(Size[2] * Spacing[2] / NewSpacing[2])]
    elif not NewSize is None and SpacingScale is None and NewSpacing is None:
        NewSpacing = [Spacing[0]*Size[0] / NewSize[0],
                      Spacing[1]*Size[1] / NewSize[1],
                      Spacing[2]*Size[2] / NewSize[2]]

    Resample = sitk.ResampleImageFilter()
    Resample.SetOutputDirection(Direction)
    Resample.SetOutputOrigin(Origin)
    Resample.SetSize(NewSize)
    Resample.SetOutputSpacing(NewSpacing)
    Resample.SetInterpolator(Interpolator)
    NewImage = Resample.Execute(Image)

    return NewImage

def _Series_dicom_reader(path):
    Reader = sitk.ImageSeriesReader()
    name = Reader.GetGDCMSeriesFileNames(path)
    Reader.SetFileNames(name)
    Image = Reader.Execute()

    image = sitk.GetArrayFromImage(Image)
    Spa = Image.GetSpacing()
    Ori = Image.GetOrigin()
    Dir = Image.GetDirection()
    return Image, image, (Spa, Ori, Dir)


def _sitk_Image_reader(path):
    Image = sitk.ReadImage(path)
    image = sitk.GetArrayFromImage(Image)
    Spa = Image.GetSpacing()
    Ori = Image.GetOrigin()
    Dir = Image.GetDirection()
    return Image, image, (Spa, Ori, Dir)


def _sitk_image_writer(image, meta, path):
    Image = sitk.GetImageFromArray(image)
    if meta is None:
        pass
    else:
        Image.SetSpacing(meta[0])
        Image.SetOrigin(meta[1])
        Image.SetDirection(meta[2])
    sitk.WriteImage(Image, path)

def load_pkl(file):
    with open(file, 'rb') as f:
        a = pkl.load(f)
    return a

def save_pkl(info, file):
    with open(file, 'wb') as f:
        pkl.dump(info, f)
