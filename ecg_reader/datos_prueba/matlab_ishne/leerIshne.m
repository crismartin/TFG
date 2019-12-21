function [holter,crcCabecera] = leerIshne(fname)
%""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
% PROPÓSITO:
% Programa que lee un archivo con registros de Holter almacenados con
% el estandar ISHNE. Formato *.ecg
%
% FORMA DE USO:
%	[holter,crcCabecera] = LeerIshne(fname);
%
% ARGUMENTOS...
% ...DE ENTRADA: 
%       .-fname ---> Nombre del fichero ISHNE-Holter.
% ...DE  SALIDA: 
%       .-holter  ---> Struct que contiene toda la informacion
%       extraida del fichero ishne, incluyendo los datos de la cabecera 
%       y los de ECG, guardados en holter.ECG y colocados todos los canales
%       en el orden del fichero ISHNE.
%       .-crcCabecera ---> Vector de bytes sin signo que contiene la
%       cabecera. Sirve para computar el crc.
%
% COMENTARIOS:
%
%
% VER TAMBIÉN:
% See also  crc16eval.m 	
%
%""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
% AUTORES:
% REBECA GOYA ESTEBAN
% OSCAR BARQUERO PEREZ
% 
% FECHA: 08-02-2007
%
% VERSION 2.0
%
% BIBLIOGRAFIA:
%   .-'The ISHNE Holter Standard Output File Format'. Fabio Badilini et al.
%A.N.E, July 1998, Vol. 3, No. 3, Part 1.
%""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
%
%
fid = fopen(fname,'r','ieee-le');

[nameholter, mode, mformat] = fopen(fid);

if (fid==-1)
    errordlg({'No se puede abrir el fichero'},'Error de fichero');
    return;
end
holter = struct('name',fname,'mn',[],'crc',[],'header',[],'ECG',[]);

%Lectura del número mágico
holter.mn = fread(fid,8,'*char')';

if(~strcmp(holter.mn,'ISHNE1.0'))
    errordlg({'El archivo no tiene formato ISHNE1.0'},'Formato no válido');
    fclose(fid);
    return;
end

%Lectura del CRC

holter.crc = fread(fid,1,'uint16');

%% COMPROBACION DEL CRC
%Para la comprobación del crc vamos a leer la cabecera como bytes y a
%guardar toda la información en un vector que llamaremos cabeceraCrc con
%formato uint8. A este vector hay que añadirle el bloque variable. Pero
%como todavia no conocemos el valor del offset ni la longitud de dicho
%bloque lo hacemos al final de la lectura de la cabecera

%Como offset para volver a esta posición despues
%leer la cabecera

OffsetCabecera = ftell(fid); 

%El bloque fijo de la cabecera tiene 512 bytes.

crcCabecera = fread(fid,512,'uint8');

%volvemos a posicionar en el comienzo de la cabecear 

fseek(fid,OffsetCabecera,'bof');
%%
%%%%%%%%HEADER%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

holter.header.var_length_block_size = fread(fid,1,'int32');

holter.header.sample_size_ECG = fread(fid,1,'int32');

holter.header.offset_var_length_block = fread(fid,1,'int32');
 
holter.header.offset_ECG_block = fread(fid,1,'int32');

holter.header.file_Version = fread(fid,1,'int16');

holter.header.First_Name = fread(fid,40,'*char')';

holter.header.Second_Name = fread(fid,40,'*char')';

holter.header.ID = fread(fid,20,'*char')';

holter.header.Sex = fread(fid,1,'int16');

holter.header.Race = fread(fid,1,'int16');

holter.header.Birth_Date = fread(fid,3,'int16');

holter.header.Record_Date = fread(fid,3,'int16'); 

holter.header.File_Date = fread(fid,3,'int16'); 

holter.header.Start_time = fread(fid,3,'int16');

holter.header.nLeads = fread(fid,1,'int16');

holter.header.Lead_Spec = fread(fid,12,'int16');

holter.header.Lead_Qual = fread(fid,12,'int16');

holter.header.Resolution = fread(fid,12,'int16');

%Aquí se podrían comparar que las resoluciones coinciden con el número de
%canales que se indican en la cabecera.

holter.header.Pacemaker = fread(fid,1,'int16');

holter.header.Recorder = fread(fid,40,'*char')';

holter.header.Sampling_Rate = fread(fid,1,'int16');

holter.header.Propierty = fread(fid,80,'*char')';

holter.header.Copyright = fread(fid,80,'*char')';

holter.header.Reserved = fread(fid,88,'*char')';

%%
%%%%%%%%%%%%%Bloque variable de la cabecera%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%Comprobacion: podriamos comprobar que la poscion en que nos encontramos
%%ahora coincide con el offset para el bloque variable

%if (holter.header.offset_var_length_block ~= ftell(fid))
%   errordlg({'El tamanho del bloque fijo es erroneo'},'Error en la
%   cabecera');
%   fclose(fid);
%   return;
%end


holter.header.var_Block = fread(fid,holter.header.var_length_block_size,'char');


%Juntamos la informacion del bloque variable a la variable que permitira
%comprobar el crc

crcCabecera = [crcCabecera,holter.header.var_Block];
%%
%%%%%%%%%%%%%%%%%%%%%%%%%Bloque de ECG%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%Comprobacion: podriamos comprobar que la poscion en que nos encontramos
%%ahora, coincide con el offset para el bloque ecg

%if (holter.header.offset_ECG_block ~= ftell(fid))
%   errordlg({'El tamanho de la cabecera es erroneo'},'Error en la
%   cabecera');
%   fclose(fid);
%   return;
%end

%inicializacion

%holter.ECG = zeros(holter.header.sample_size_ECG/holter.header.nLeads,holter.header.nLeads);

%%%Lectura completa de los datos de ECG

holter.ECG = fread(fid,'int16');

%%%Optamos por no separar los canales, esto mejor hacerlo cuando se vayan a
%%%presentar los resultados tomando nLeads
%%%
    


%Cerramos el fichero
fclose(fid);

