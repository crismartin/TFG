function escribirIshne(holter)
%""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
% PROPÓSITO:
% Programa que escribe un archivo binario en formato Ishne a partir
% de un struct que contiene toda la información cabecera, ECG y checksum
%
% FORMA DE USO:
%	escribirIshne(holter);
%
% ARGUMENTOS...
% ...DE ENTRADA: 
%       .-holter ---> struct con toda la información para poder escribir un
% ishne..
% ...DE  SALIDA: 
%       .-
%
% COMENTARIOS:
% Se crea un archivo con extensión .ecg en el directorio actual (current 
% directory)   
%
% VER TAMBIÉN:
% See also leerIshne	
%
%""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
% AUTORES:
% REBECA GOYA ESTEBAN
% OSCAR BARQUERO PEREZ
% 
% FECHA: 12-02-2007
%
% VERSION 2.0
%
% BIBLIOGRAFIA:
%   .-
%""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
%
%



fid = fopen([holter.name,'.ecg'],'w','ieee-le');
%%
%
%Escritura del fichero binario

%MagicNumber
fwrite(fid,holter.mn,'char');

%crc
fwrite(fid,holter.crc,'uint16');

fwrite(fid,holter.header.var_length_block_size,'int32');

fwrite(fid,holter.header.sample_size_ECG,'int32');

fwrite(fid,holter.header.offset_var_length_block,'int32');

fwrite(fid,holter.header.offset_ECG_block,'int32');

fwrite(fid,holter.header.file_Version,'int16');

fwrite(fid,holter.header.First_Name,'char');

fwrite(fid,holter.header.Second_Name,'char');

fwrite(fid,holter.header.ID,'char');

fwrite(fid,holter.header.Sex,'int16');

fwrite(fid,holter.header.Race,'int16');

fwrite(fid,holter.header.Birth_Date,'int16');

fwrite(fid,holter.header.Record_Date,'int16');

fwrite(fid,holter.header.File_Date,'int16');

fwrite(fid,holter.header.Start_time,'int16');

fwrite(fid,holter.header.nLeads,'int16');

fwrite(fid,holter.header.Lead_Spec,'int16');

fwrite(fid,holter.header.Lead_Qual,'int16');

fwrite(fid,holter.header.Resolution,'int16');

fwrite(fid,holter.header.Pacemaker,'int16');

fwrite(fid,holter.header.Recorder,'char');

fwrite(fid,holter.header.Sampling_Rate,'int16');

fwrite(fid,holter.header.Propierty,'char');

fwrite(fid,holter.header.Copyright,'char');

fwrite(fid,holter.header.Reserved,'char');

fwrite(fid,holter.ECG,'int16');

fclose(fid);